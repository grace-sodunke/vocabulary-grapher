document.addEventListener('DOMContentLoaded', (event) => {
    const projectorIframe = document.getElementById("projector");
    projectorIframe.src = "projector_url";
    generateTextBoxes();  // Generate initial set of text boxes
});

function generateTextBoxes() {
    const numberOfAxes = parseInt(document.getElementById("axesSelector").value, 10);
    const textBoxContainer = document.getElementById("textBoxContainer");

    // Clear existing text boxes
    textBoxContainer.innerHTML = "";

    // Generate new text boxes
    for (let i = 1; i <= numberOfAxes; i++) {
        const input = document.createElement("input");
        input.type = "text";
        input.name = "axis" + i;
        input.className = "form-control mt-2";
        input.placeholder = "Axis Word " + i;
        textBoxContainer.appendChild(input);
    }
}

document.getElementById("resetButton").addEventListener("click", function() {
    // Resets form fields to initial values
    document.getElementById("myForm").reset();

    // Reset dynamically generated text boxes
    const textBoxContainer = document.getElementById("textBoxContainer");
    const textboxes = textBoxContainer.getElementsByTagName("input");
    
    for(let i = 0; i < textboxes.length; i++) {
        textboxes[i].value = "";
    }
});
