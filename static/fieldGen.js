window.onload = function() {
	var fdButton = document.getElementById("add-field-button");
	fdButton.disabled = false;
	fdButton.onclick = function() { genField(2) };
}

function genField(num) {
	var prevFieldDescriptionNum = num - 1;
	var prevFieldDescriptionId = prevFieldDescriptionNum.toString() + "-field-description";
	var prevFieldDescription = document.getElementById(prevFieldDescriptionId);

	var fdDiv = document.createElement("div");
	fdDivNum = num.toString();
	fdDiv.id = fdDivNum + "-field-description";

	var fieldLabelText = document.createTextNode("Field Label:");
	fdDiv.appendChild(fieldLabelText);
	fdDiv.appendChild(document.createElement("br"));

	var fdLabel = document.createElement("input");
	fdLabel.type = "text";
	fdLabel.name = num + "-field-label";
	fdDiv.appendChild(fdLabel);
	fdDiv.appendChild(document.createElement("br"));

	var fieldKindText = document.createTextNode("Field Kind:");
	fdDiv.appendChild(fieldKindText);
	fdDiv.appendChild(document.createElement("br"));

	var fdSelect = document.createElement("select");
	fdSelect.name = num + "-field-kind";

	var fdShortTextOption = document.createElement("option");
	fdShortTextOption.value = "short_text";
	fdShortTextOption.innerHTML += "Short Text";
	fdSelect.appendChild(fdShortTextOption);

	var fdLongTextOption = document.createElement("option");
	fdLongTextOption.value = "long_text";
	fdLongTextOption.innerHTML += "Long Text";
	fdSelect.appendChild(fdLongTextOption);

	var fdDropDownOption = document.createElement("option");
	fdDropDownOption.value = "drop_down";
	fdDropDownOption.innerHTML += "Drop Down Menu";
	fdSelect.appendChild(fdDropDownOption);

	var fdCheckBoxOption = document.createElement("option");
	fdCheckBoxOption.value = "check_box";
	fdCheckBoxOption.innerHTML += "Check Box List";
	fdSelect.appendChild(fdCheckBoxOption);

	var fdRadioOption = document.createElement("option");
	fdRadioOption.value = "radio";
	fdRadioOption.innerHTML += "Radio List";
	fdSelect.appendChild(fdRadioOption);

	fdDiv.appendChild(fdSelect);
	fdDiv.appendChild(document.createElement("br"));

	var fdButton = document.getElementById("add-field-button");
	var nextFieldDescriptionNum = num + 1;
	fdButton.onclick = function() { genField( nextFieldDescriptionNum) };
	
	prevFieldDescription.parentNode.insertBefore(fdDiv, prevFieldDescription.nextSibling);
}