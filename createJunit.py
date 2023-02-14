import xml.etree.ElementTree as ET

junit_data = {'testResults': {'@version': '1.2', 'httpSample': {'@t': '2563', '@it': '0', '@lt': '2560', '@ct': '2266', '@ts': '1675683480239', '@s': 'true', '@lb': 'GetBusinessByName', '@rc': '200', '@rm': 'OK', '@tn': 'Thread Group 1-1', '@dt': 'text', '@by': '12272', '@sby': '221', '@ng': '1', '@na': '1', 'java.net.URL': 'https://businessldstage.azurewebsites.net/api/businessdetail/dev?code=YMNBqPvshxRpljE0kjNam5XI7eIOXU1PSnH6G/o4y1pQCnAT5CLXuw=='}}}      

root = ET.Element('testsuites')
suite = ET.SubElement(root, 'testsuite', name='example')
print(len(junit_data['testResults']))
print(junit_data['testResults'])
for case in junit_data['testResults']['httpSample']:
    #print(junit_data['testResults']['httpSample'][case])
    ET.SubElement(suite, 'testcase', ib=junit_data['testResults']['httpSample']['@lb'], timetaken=junit_data['testResults']['httpSample']['@ts'])

tree = ET.ElementTree(root)
tree.write('junit.xml')