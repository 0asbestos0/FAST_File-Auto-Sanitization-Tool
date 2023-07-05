import vt
import time
client = vt.Client("749af937f197839a0454696804dd82d16e4819ab9fe5fd63587896a887f2bf73")


with open("C:\\Users\\husky\\Downloads\\malpdf.pdf", "rb") as f:
	analysis = client.scan_file(f)

while True:
	analysis = client.get_object("/analyses/{}", analysis.id)
	print(analysis.status)
	if analysis.status == "completed":
		break
	time.sleep(30)

print(client.get_object("/analyses/{}", analysis.id))
print(analysis.results.keys())
results=[]
for val in analysis.results.values():
	results.append(val['result'])
positives=0
for result in results:
	if result!=None:
		positives=positives+1

print(str(positives)+'/'+str(len(results))+' engines flagged it as MALICIOUS')
client.close()