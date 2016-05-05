// Used to uniquely identify each option input for a given field, needed in order to use the <label> tag.
var optionCounter = 0;

// Delete any option inputs assigned to a given field template. Called whenever a new field kind is selected.
function delOptions(fdNum) {
    var addOptionBtn = document.getElementById(fdNum + "-add-option-btn");
    if (addOptionBtn !== null) {
        addOptionBtn.parentNode.removeChild(addOptionBtn);
    }
    var optionFieldDivs = document.getElementsByClassName(fdNum + "-option-field-div");
    while (optionFieldDivs.length > 0) {
        optionFieldDivs[0].parentNode.removeChild(optionFieldDivs[0]);
    }
}

// Gen option is called whenever a new field kind is selected. If the field kind is one that requires options (dropdown, checkbox, radio list), it creates an <input> for the respective field template, is given a unique identifier, and a button to create additional <input> tags, for a variable number of options per field template.
function genOption(fdNum) {
    // Get field kind that triggered genOption()
    var fkSelectId = fdNum + "-field-kind-select";
    var fkSelect = document.getElementById(fkSelectId);
    var currentVal = fkSelect.value;

    // If field kind is one that requires an option input, create an option input and assign it fdNum as the group identifier.
    if (currentVal === "drop_down" || currentVal === "check_box" || currentVal === "radio") {
        // Increase optionCounter, so that a unique identifier can be placed for each option field generated.
        optionCounter += 1;

        // Wrapper for the option input, assigned fdNum as group identifier.
        var optionFieldDiv = document.createElement("div");
        optionFieldDiv.className = fdNum + "-option-field-div";

        // MDL styling for option input
        var styledOptionLabelContainer = document.createElement("div");
        styledOptionLabelContainer.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";

        // <label> tag assigned to option input, with MDL styling. Current integer in optionCounter is assigned as unique identifier for the option input so that the <label> tag may be assigned.
        var optionLabelSubtitle = document.createElement("label");
        optionLabelSubtitle.htmlFor = optionCounter + "-option-input";
        optionLabelSubtitle.className = "mdl-textfield__label";
        optionLabelSubtitle.innerHTML = "Option Label";
        styledOptionLabelContainer.appendChild(optionLabelSubtitle);

        // Option <input> tag, with unique number as identifier (for <label> tag) and fdNum assigned as group identifier (for it's respectiv Field Template).
        var optionInput = document.createElement("input");
        optionInput.name = fdNum + "-option";
        optionInput.id = optionCounter + "-option-input";
        optionInput.className = fdNum + "-option-input mdl-textfield__input";
        styledOptionLabelContainer.appendChild(optionInput);

        // Material Design Lite will automatically register and render all elements marked with MDL classes upon page load.
        // However in the case where you are creating DOM elements dynamically you need to register new elements using the upgradeElement function.
        componentHandler.upgradeElement(styledOptionLabelContainer);
        optionFieldDiv.appendChild(styledOptionLabelContainer);

        var fdDiv = document.getElementById(fdNum + "-field-description");

        // Button to create any addition option inputs for the field template. Assigned fdNum as group identifier, and styled as an icon using MDL.
        var addOptionBtn = document.getElementById(fdNum + "-add-option-btn");
        if (addOptionBtn == null) {
            addOptionBtn = document.createElement("button");
            addOptionBtn.type = "button";
            addOptionBtn.id = fdNum + "-add-option-btn";
            addOptionBtn.className = "mdl-button mdl-js-button mdl-button--icon";
            addOptionBtn.onclick = function() { genOption(fdNum) };

            // Tag to identify icon type for MDL styling.
            addOptionIcon = document.createElement("i");
            addOptionIcon.className = "material-icons";
            addOptionIcon.innerHTML = "add_circle_outline";
            addOptionBtn.appendChild(addOptionIcon);

            fdDiv.appendChild(addOptionBtn);
        }

        fdDiv.insertBefore(optionFieldDiv, addOptionBtn);

        // This will add a button to remove the option input (in case the user decides they have created too many option inputs for a given field template). This will only apply if this is the second or greater (not the first) option input for the field template (drop down, checkbox, and radio list field kinds require at least one option assigned). Styled as icon with MDL.
        var fdOptionInputs = document.getElementsByClassName(fdNum + "-option-input");
        if (fdOptionInputs.length > 1) {
            var removeOptionBtn = document.createElement("button");
            removeOptionBtn.type = "button";
            removeOptionBtn.className = fdNum + "-remove-option-btn mdl-button mdl-js-button mdl-button--icon";
            removeOptionBtn.onclick = function() {
                optionFieldDiv.parentNode.removeChild(optionFieldDiv);
            }

            // Tag to identify the icon type for MDL.
            var removeOptionIcon = document.createElement("i");
            removeOptionIcon.className = "material-icons";
            removeOptionIcon.innerHTML = "remove";
            removeOptionBtn.appendChild(removeOptionIcon);

            optionFieldDiv.appendChild(removeOptionBtn);
        }
    } else {
        delOptions(fdNum);
    }
}

// Generate inputs for additional field template for the record template.
function genField(fdNum) {
    // Div wrapper to contain field template inputs, with fdNum assigning a unique, group identifier for the div
    var fdDiv = document.createElement("div");
    fdDivNum = fdNum.toString();
    fdDiv.id = fdDivNum + "-field-description";

    // Div wrapper for MDL styling
    var styledFieldLabelContainer = document.createElement("div");
    styledFieldLabelContainer.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";

    // <label> tag for the "field label" with MDL styling, assigned fdNum as group identifier
    var fdLabelSubtitle = document.createElement("label");
    fdLabelSubtitle.htmlFor = fdNum + "-field-label";
    fdLabelSubtitle.className = "mdl-textfield__label";
    fdLabelSubtitle.innerHTML = "Field Label";
    styledFieldLabelContainer.appendChild(fdLabelSubtitle);

    // <input> tag for the "field label" with MDL styling, assigned fdNum as group identifier
    var fdLabelInput = document.createElement("input");
    fdLabelInput.type = "text";
    fdLabelInput.name = fdNum + "-field-label";
    fdLabelInput.id = fdNum + "-field-label";
    fdLabelInput.className = "mdl-textfield__input";
    styledFieldLabelContainer.appendChild(fdLabelInput);

    // Material Design Lite (MDL) will automatically register and render all elements marked with MDL classes upon page load.
    // However in the case where you are creating DOM elements dynamically you need to register new elements using the upgradeElement function. 
    componentHandler.upgradeElement(styledFieldLabelContainer);

    fdDiv.appendChild(styledFieldLabelContainer);

    // Button to remove the field template (in case the user decides they have created more than they find necessary). Styled as icon with MDL.
    var removeFieldBtn = document.createElement("button");
    removeFieldBtn.type = "button";
    removeFieldBtn.id = fdNum + "-remove-field-div-btn";
    removeFieldBtn.className = "mdl-button mdl-js-button mdl-button--icon";
    removeFieldBtn.onclick = function() {
        fdDiv.parentNode.removeChild(fdDiv);
    }

    // Turns removeFieldBtn into an 'icon' button using MDL styling.
    var removeFieldIcon = document.createElement("i");
    removeFieldIcon.className = "material-icons";
    removeFieldIcon.innerHTML = "remove";
    removeFieldBtn.appendChild(removeFieldIcon);

    fdDiv.appendChild(removeFieldBtn);

    fdDiv.appendChild(document.createElement("br"));

    var fieldKindText = document.createTextNode("Field Kind:");
    fdDiv.appendChild(fieldKindText);

    fdDiv.appendChild(document.createElement("br"));

    // Drop down so the user can choose field kind, assigned fdNum as unique group identfier
    var fdSelect = document.createElement("select");
    fdSelect.name = fdNum + "-field-kind";
    fdSelect.id = fdNum + "-field-kind-select";
    // On change, any option inputs assigned are removed (if any), and if the field kind chosen is one that requires options (drop down, checkbox, radio list), a new option input is generated with fdNum as unique group identifier.
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

    // Button to add an additional field template for the record template. fdNum + 1 is assigned for the unique group identifier for the next field template.
    var addFieldButton = document.getElementById("add-field-button");
    var nextFdNum = fdNum + 1;
    addFieldButton.onclick = function() { genField(nextFdNum); };

    var fdContainer = document.getElementById("field-descriptions");
    fdContainer.appendChild(fdDiv);
}

// Initialize functions for add field, which will add an addition Field Label and Field Kind with a unique div id, and field kind select which will add inputs for options if appropriate (if field kind is checkbox, radio list, and drop down)
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