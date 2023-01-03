var xhr = new XMLHttpRequest();
var count = -1; // start out with a value that is obviously wrong, so we know if it doesn't change

xhr.onreadystatechange = function() {
  if (xhr.readyState === 4 && xhr.status === 200) {
    console.log(xhr.responseText);
  }
};

console.log("Beginning POST request to API Gateway")
xhr.open('POST', 'https://ig8y19eu4m.execute-api.us-east-1.amazonaws.com/prod');
xhr.withCredintials = true;
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send(JSON.stringify({ 
    "operation": "update",
    "payload": {
                "Item": {
                        "id": "myCount",
                        "attribute": "visCount",
                        "expression": "++"
                        }
                }
    }));
console.log("POST request to API Gateway completed for incrementing the visitor count");

xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
  if (xhr.readyState === 4 && xhr.status === 200) {
    var response = JSON.parse(xhr.responseText)
    console.log(xhr.response);
    var message = response.message;
    var messageArray = message.split(' ')
    count = messageArray[7]
    console.log(count)
    document.getElementById("visCount").innerHTML=count;
  }
};
xhr.open('POST', 'https://ig8y19eu4m.execute-api.us-east-1.amazonaws.com/prod');
xhr.withCredintials = true;
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send(JSON.stringify({
    "operation": "read",
    "payload": {
                "Item": {
                        "id": "myCount",
                        "attribute": "visCount"
                        }
                }
}));
console.log("POST request to the API Gateway completed for reading the visitor count");
