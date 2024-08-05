import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import io

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == '9702/41/w20/3':
        q = input("Input exam and question in the format code/paper/session/question ex: 9702/41/s19/3: \n")
        code = q[0:4]
        paper = q[5:7]
        sess = q[8:11]
        question = q[12:]
        response = requests.get(f"https://dynamicpapers.com/wp-content/uploads/2015/09/{code}_{sess}_ms_{paper}.pdf")
        from pypdf import PdfReader
        string = ""
        on_fly = io.BytesIO(response.content)
        reader = PdfReader(on_fly)
        for page in reader.pages:
            string = string + page.extract_text()
        z = 0
        l =0 
        end = []
        while l != -1:
            k=string.find("9702",z+1)
            l=string.find("Marks",z+1)
            if k != -1:
                end.append(k)
                end.append(l)
            z = l
        newstr = ""
        j = 0
        for i in range(0,len(end),2):
            k = end[i]
            newstr = "".join([newstr,string[j:k]])
            j = end[i+1]
        string = "".join([newstr,string[j:]])
        i=1
        index = []
        j = string.find("".join([str(i),"("])) 
        string = string[j:]
        j = string.find("".join([str(i),"("])) 
        while j != -1:
            index.append(j)
            i+=1
            j = string.find("".join([str(i),"("])) 
        print(i)
        print(len(index))
        if int(question) > i-1:
            print(f"Invalid question exam only has {i-1} questions")
        elif int(question) == i-1:
            print(string[-1:])
        else:
            n = int(question)
        resp.message("string[index[n-1]:index[n]]")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
