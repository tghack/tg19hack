const rooturl = window.location.protocol+"//"+window.location.host+"/";

var barcodeBuffer = "";

document.getElementById("clearTableBarcode").onclick = function () {
	location.reload()
}

document.addEventListener("keydown", function(e) {
	var key = e.key

	if (key == 'Shift' || key == 'Alt' || key == "Control" )
		return;

	if (key != 'Enter') {
		barcodeBuffer += key
		return;
	}

	if (barcodeBuffer == "clrtbl") 
		location.reload()

	const inputBody = { 'id': `'${barcodeBuffer}'` }

	const userAction = async () => {
		const response = await fetch(`${rooturl}wand`, {
			method: 'POST',
			body: JSON.stringify(inputBody),
			headers:{
				'Content-Type': 'application/json'
			}
		});
		const res = await response.json()
		console.log('response: ', res) 

		if (res.message == '500: Internal server error') {
			document.getElementById("messageBox").innerHTML = 'Oops.. Something went wrong.'
			return;
		}

		if (res.message){
			document.getElementById("messageBox").innerHTML = res.message
			return;
		}

		var table = document.getElementById("wandTable")
		var wands = res.result;

		var x;
		for (x in wands) {
			var row = table.insertRow(1)
			var idCell = row.insertCell(0)
			var nameCell = row.insertCell(1)
			var descCell = row.insertCell(2)

			idCell.innerHTML = wands[x].id
			nameCell.innerHTML = wands[x].name
			descCell.innerHTML = wands[x].description
		}
	}	
  
	userAction()
	  
	barcodeBuffer = ""
})
