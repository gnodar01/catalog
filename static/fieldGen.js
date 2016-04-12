function genOption(num){
	var fkSelectId = num + "-field-kind-select";
	var fkSelect = document.getElementById(fkSelectId);
	var currentVal = fkSelect.value;
	
	var currentOptionFieldDivs = document.getElementsByClassName(num + "-option-field-div");

	if (currentVal === "drop_down" || currentVal === "check_box" || currentVal === "radio") {
		if(currentOptionFieldDivs.length === 0) {
			var fieldDescriptionDiv = document.getElementById(num + "-field-description");

			var newOptionButton = document.getElementById(num + "-new-option-button");
			if (newOptionButton == null) {
				newOptionButton = document.createElement("button");
				newOptionButton.type = "button";
				newOptionButton.id = num + "-new-option-button";
				newOptionButton.innerHTML = "Add option";
				newOptionButton.onclick = function() { genOption(num) };

				fieldDescriptionDiv.appendChild(newOptionButton);
			}

			var optionFieldDiv = document.createElement("div");
			optionFieldDiv.className = num + "-option-field-div";

			var optionInput = document.createElement("input");
			optionInput.name = num + "-option";
			optionInput.class = num + "-option-input";
			var optionInputText = document.createTextNode("Option Label:");

			optionFieldDiv.appendChild(optionInputText);
			optionFieldDiv.appendChild(document.createElement("br"));
			optionFieldDiv.appendChild(optionInput);
			optionFieldDiv.appendChild(document.createElement("br"));

			fieldDescriptionDiv.insertBefore(optionFieldDiv, newOptionButton);
		}
	} else {
		var newOptionButton = document.getElementById(num + "-new-option-button");
		if (newOptionButton != null) {
			newOptionButton.parentNode.removeChild(newOptionButton);
		}
		var optionFieldDivs = document.getElementsByClassName(num + "-option-field-div");
		while (optionFieldDivs.length > 0) {
			optionFieldDivs[0].parentNode.removeChild(optionFieldDivs[0]);
		}
	}
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
	fdSelect.id = num + "-field-kind-select";
	fdSelect.onchange = function() { genOption(num) };

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

	var addFieldButton = document.getElementById("add-field-button");
	var nextFieldDescriptionNum = num + 1;
	addFieldButton.onclick = function() { genField( nextFieldDescriptionNum) };
	
	prevFieldDescription.parentNode.insertBefore(fdDiv, prevFieldDescription.nextSibling);
}

window.onload = function() {
	var addFieldButton = document.getElementById("add-field-button");
	addFieldButton.disabled = false;
	addFieldButton.onclick = function() { genField(2) };

	var fieldKindSelect = document.getElementById("1-field-kind-select");
	fieldKindSelect.onchange = function() { genOption(1) };
}