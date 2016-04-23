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
		var fdDiv = document.getElementById(fdNum + "-field-description");

		var addOptionBtn = document.getElementById(fdNum + "-add-option-btn");
		if (addOptionBtn == null) {
			addOptionBtn = document.createElement("button");
			addOptionBtn.type = "button";
			addOptionBtn.id = fdNum + "-add-option-btn";
			addOptionBtn.innerHTML = "Add option";
			addOptionBtn.onclick = function() { genOption(fdNum) };

			fdDiv.appendChild(addOptionBtn);
		}

		var optionFieldDiv = document.createElement("div");
		optionFieldDiv.className = fdNum + "-option-field-div";

		var optionInputText = document.createTextNode("Option Label:");
		optionFieldDiv.appendChild(optionInputText);

		optionFieldDiv.appendChild(document.createElement("br"));

		var optionInput = document.createElement("input");
		optionInput.name = fdNum + "-option";
		optionInput.className = fdNum + "-option-input";
		optionFieldDiv.appendChild(optionInput);

		fdDiv.insertBefore(optionFieldDiv, addOptionBtn);

		var fdOptionInputs = document.getElementsByClassName(fdNum + "-option-input");
		if (fdOptionInputs.length > 1) {
			var removeOptionBtn = document.createElement("button");
			removeOptionBtn.type = "button";
			removeOptionBtn.innerHTML = "Remove Option";
			removeOptionBtn.className = fdNum + "-remove-option-btn";
			removeOptionBtn.onclick = function() {
				optionFieldDiv.parentNode.removeChild(optionFieldDiv);
			}
			optionFieldDiv.appendChild(removeOptionBtn);
		}
	} else {
		delOptions(fdNum);
	}
}

function genField(fdNum) {
	console.dir(componentHandler)

	var fdDiv = document.createElement("div");
	fdDivNum = fdNum.toString();
	fdDiv.id = fdDivNum + "-field-description";

	var styledFieldLabelContainer = document.createElement("div");
	styledFieldLabelContainer.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";

	var fdLabelSubtitle = document.createElement("label");
	fdLabelSubtitle.htmlFor = fdNum + "-field-label";
	fdLabelSubtitle.className = "mdl-textfield__label";
	fdLabelSubtitle.innerHTML = "Field Label";
	styledFieldLabelContainer.appendChild(fdLabelSubtitle);

	var fdLabelInput = document.createElement("input");
	fdLabelInput.type = "text";
	fdLabelInput.name = fdNum + "-field-label";
	fdLabelInput.id = fdNum + "-field-label";
	fdLabelInput.className = "mdl-textfield__input";
	styledFieldLabelContainer.appendChild(fdLabelInput);

	// Material Design Lite will automatically register and render all elements marked with MDL classes upon page load.
	// However in the case where you are creating DOM elements dynamically you need to register new elements using the upgradeElement function. 
	componentHandler.upgradeElement(styledFieldLabelContainer);

	fdDiv.appendChild(styledFieldLabelContainer);

	var removeFieldBtn = document.createElement("button");
	removeFieldBtn.type = "button";
	removeFieldBtn.id = fdNum + "-remove-field-div-btn";
	removeFieldBtn.className = "mdl-button mdl-js-button mdl-button--icon";
	removeFieldBtn.onclick = function() {
		fdDiv.parentNode.removeChild(fdDiv);
	}

	var removeFieldIcon = document.createElement("i");
	removeFieldIcon.className = "material-icons";
	removeFieldIcon.innerHTML = "remove";
	removeFieldBtn.appendChild(removeFieldIcon);

	fdDiv.appendChild(removeFieldBtn);

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
	var nextFdNum = fdNum + 1;
	addFieldButton.onclick = function() { genField(nextFdNum); };

	var fdContainer = document.getElementById("field-descriptions");
	fdContainer.appendChild(fdDiv);
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