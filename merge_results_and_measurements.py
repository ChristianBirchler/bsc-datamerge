#!/usr/bin/python3

import pandas as pd
import xml.etree.ElementTree as ET
import os

def get_result_from_surefire_xml(xml_path, test_identifer):
    has_skipped = False
    has_failure = False
    has_error = False
    test_is_present = False

    # get method name firse
    cnt = 0
    for char in test_identifer[::-1]:
        if char == '.': break
        cnt = cnt + 1

    test_method_name = test_identifer[-cnt:]

    # parse xml file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # check if test case was a failure or error
    for el in root.getchildren():
        # get the testcase tag
        if el.tag == "testcase":
            # look for the test method of interest
            if el.attrib["name"] == test_method_name:
                test_is_present = True
                for child in el.getchildren():
                    if child.tag == "failure": has_failure = True
                    elif child.tag == "error": has_error = True
                    elif child.tag == "skipped": has_skipped = True

    if has_failure: return "FAILED"
    if has_error: return "ERROR"
    if has_skipped: return "SKIPPED"
    if not test_is_present: return "UNKNOWN"

    return "PASSED"
    


def get_class_identifier(test_identifer):
    """
    return: return identfier till las '.'
    """
    cnt = 0
    for char in test_identifer[::-1]:
        cnt = cnt + 1
        if char == ".":
            break

    return test_identifer[0:-cnt]


def get_xml_file_path(abs_dir_path, identifer):
    """
    return path as string
    """
    class_identifier = get_class_identifier(identifer)

    file_of_interest = None
    for root, dirs, files in os.walk(abs_dir_path):
        for file in files:
            if file[-4:] == ".xml" and identifer in file:
                #print(file)
                file_of_interest = file
            elif file[-4:] == ".xml" and class_identifier in file:
                #print(file)
                file_of_interest = file

    return abs_dir_path + "/" + file_of_interest


def get_test_result(identifer, project_name, commit_hash, iteration):
    """
    This function returns the test result (P/F/U) of a test case
    identified by following arguments:
        - identifier: path to test case (e.g., ch.chribir.package.myclass.mymethod)
        - project_name: name of the project (e.g., hadoop); is used to find the surefire reports
        - commit_hash: commit hash of the version which was checked out
        - iteration: the according test run (e.g., test suite is executed 10 times then
                     'iter' can be between 0 and 10)
    """

    folder_of_interest = project_name + "_" + commit_hash + "_" + str(iteration)

    test_result = 'NOT FOUND'

    try:
        xml_file_path = get_xml_file_path(SUREFIRE_REPORTS_PATH+'/'+folder_of_interest, identifer)
        test_result = get_result_from_surefire_xml(xml_file_path, identifer)
    except:
        print("report not found of: "+str(identifer)+"\thash="+str(commit_hash)+"\titer="+str(iteration))


    # for root, dirs, files in os.walk(SUREFIRE_REPORTS_PATH):
    #     for dir in dirs:
    #         if dir == folder_of_interest:
    #             #print("FOUND:" + folder_of_interest)
                
    #             abs_dir_path = root + "/" + folder_of_interest
    #             try:
    #                 xml_file_path = get_xml_file_path(abs_dir_path, identifer)
    #                 #print(identifer)
    #                 #print(xml_file_path)
    #                 test_result = get_result_from_surefire_xml(xml_file_path, identifer)
    #             except:
    #                 print("report not found of: "+str(identifer)+"\thash="+str(commit_hash)+"\titer="+str(iteration))

    return test_result


if __name__ == "__main__":

    # print(get_result_from_surefire_xml("/home/christian/Desktop/my-app/target/surefire-reports/TEST-ch.chribir.AppTest.xml", "ch.chribir.AppTest.testZero"))
    # print(get_result_from_surefire_xml("/home/christian/Desktop/my-app/target/surefire-reports/TEST-ch.chribir.AppTest.xml", "ch.chribir.AppTest.testOne"))
    # print(get_result_from_surefire_xml("/home/christian/Desktop/my-app/target/surefire-reports/TEST-ch.chribir.AppTest.xml", "ch.chribir.AppTest.testTwo"))
    # print(get_result_from_surefire_xml("/home/christian/Desktop/my-app/target/surefire-reports/TEST-ch.chribir.AppTest.xml", "ch.chribir.AppTest.testThree"))

    """
    - create new column/variable named pass/fail
    - iterate over entries (PrimaryKey(TestCase, iteration))
    - search in surefire reports the according test result
    - insert the tests result into the data set
    """

    ######### PARAMETERS ##########
    ROOT = os.getcwd()
    MEASUREMENT_PATH = ROOT+"/measurements.csv"
    SUREFIRE_REPORTS_PATH = ROOT+"/16052020_VM6_SOURCETRANS_V2_NO-GC/surefire-results"
    OUTPUT_FILE_PATH = ROOT+"/data-merge-output.csv"
    RED='\033[0;31m'
    NC='\033[0m'
    ######### PARAMETERS ##########

    print(RED+"merge jvm metrics with the surefire reports ..."+NC)

    #load data set
    dd = pd.read_csv(MEASUREMENT_PATH)

    #print(dd.iloc[0,0])

    # insert new column for test outcome; default "U"=Unknown
    dd.insert(1, "pass/fail", None)
    #print(dd.head())

    test_identifier = None
    test_iteration = None
    for i in range(len(dd)):
        test_identifier = dd.iloc[i,0]
        test_project_name = dd.iloc[i,2]
        test_commit_hash = dd.iloc[i,3]
        test_iteration = dd.iloc[i,4]
        #print(test_identifier + " " + str(test_iteration))

        # look for the test result
        test_result = get_test_result(test_identifier, test_project_name, test_commit_hash, test_iteration)

        # add test result to data frame
        dd.iloc[i,1] = test_result
        print("line="+str(i)+"\ttest="+str(test_identifier)+"\tresult="+str(test_result))
        #print(dd.iloc[i,1])

    #print( dd.loc[ dd['pass/fail']=="NOT FOUND" ] )
    print("write csv ...")
    dd.to_csv(OUTPUT_FILE_PATH)


    print(RED+"merge completed ..."+NC)
