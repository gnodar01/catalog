function delOptions(fdNum) {
	var addOptionBtn = document.getElementById(fdNum + "-add-option-btn");
	if (addOptionBtn != null) {
		addOptionBtn.parentNode.removeChild(addOptionBtn);
	}
	var optionFieldDivs = document.getElementsByClassName(fdNum + "-option-field-div");
	while (optionFieldDivs.length > 0) {
		optionFieldDivs[0].parentNode.removeChild(optionFieldDivs[0]);
	}
}

function genOption(fdNum){
	var fkSelectId = fdNum + "-field-kind-select";
	var fkSelect = document.getElementById(fkSelectId);
	var currentVal = fkSelect.value;

	if (currentVal === "drop_down" || currentVal === "check_box" || currentVal === "radio")  {
		var fieldDescriptionDiv = document.getElementById(fdNum + "-field-description");

		var addOptionBtn = document.getElementById(fdNum + "-add-option-btn");
		if (addOptionBtn == null) {
			addOptionBtn = document.createElement("button");
			addOptionBtn.type = "button";
			addOptionBtn.id = fdNum + "-add-option-btn";
			addOptionBtn.innerHTML = "Add option";
			addOptionBtn.onclick = function() { genOption(fdNum) };

			fieldDescriptionDiv.appendChild(addOptionBtn);
		}

		var optionFieldDiv = document.createElement("div");
		optionFieldDiv.className = fdNum + "-option-field-div";

		var optionInput = document.createElement("input");
		optionInput.name = fdNum + "-option";
		optionInput.class = fdNum + "-option-input";
		var optionInputText = document.createTextNode("Option Label:");

		optionFieldDiv.appendChild(optionInputText);
		optionFieldDiv.appendChild(document.createElement("br"));
		optionFieldDiv.appendChild(optionInput);
		optionFieldDiv.appendChild(document.createElement("br"));

		fieldDescriptionDiv.insertBefore(optionFieldDiv, addOptionBtn);
	} else {
		delOptions(fdNum);
	}
}

function genField(fdNum) {
	var prevFieldDescriptionNum = fdNum - 1;
	var prevFieldDescriptionId = prevFieldDescriptionNum.toString() + "-field-description";
	var prevFieldDescription = document.getElementById(prevFieldDescriptionId);

	var fdDiv = document.createElement("div");
	fdDivNum = fdNum.toString();
	fdDiv.id = fdDivNum + "-field-description";

	var fieldLabelText = document.createTextNode("Field Label:");
	fdDiv.appendChild(fieldLabelText);
	fdDiv.appendChild(document.createElement("br"));

	var fdLabel = document.createElement("input");
	fdLabel.type = "text";
	fdLabel.name = fdNum + "-field-label";
	fdDiv.appendChild(fdLabel);
	fdDiv.appendChild(document.createElement("br"));

	var fieldKindText = document.createTextNode("Field Kind:");
	fdDiv.appendChild(fieldKindText);
	fdDiv.appendChild(document.createElement("br"));

	var fdSelect = document.createElement("select");
	fdSelect.name = fdNum + "-field-kind";
	fdSelect.id = fdNum + "-field-kind-select";
	fdSelect.onchange = function() {
		delOptions(fdNum);
		genOption(fdNum);
	};

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
	var nextFieldDescriptionNum = fdNum + 1;
	addFieldButton.onclick = function() { genField(nextFieldDescriptionNum); };
	
	prevFieldDescription.parentNode.insertBefore(fdDiv, prevFieldDescription.nextSibling);
}

window.onload = function() {
	var addFieldButton = document.getElementById("add-field-button");
	addFieldButton.disabled = false;
	addFieldButton.onclick = function() { genField(2) };

	var fieldKindSelect = document.getElementById("1-field-kind-select");
	fieldKindSelect.onchange = function() {
		delOptions(1);
		genOption(1);
	};
}