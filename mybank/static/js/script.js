function populate(object){
let html_data=`<h3>${object.balance}</h3>`

document.querySelector("#result").innerHTML=html_data;
}
function getBalance(){
fetch('http://127.0.0.1:8000/enq').
then(res=>res.json()).then(data=>alert('Account Balance : '+data.balance)).
catch(err=>console.log(err));
}