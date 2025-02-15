document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript Loaded");
});

function uploadImage() {
    let fileInput = document.getElementById("imageUpload");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select an image.");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.ingredients) {
            displayIngredients(data.ingredients);
        } else {
            alert("No ingredients detected.");
        }
    })
    .catch(error => console.error("Error:", error));
}

function displayIngredients(ingredients) {
    let grid = document.getElementById("ingredientsGrid");
    grid.innerHTML = ""; // Clear existing items

    ingredients.forEach(ingredient => {
        let ingredientCard = document.createElement("div");
        ingredientCard.classList.add("ingredient-card");

        let image = document.createElement("img");
        image.src = `https://www.themealdb.com/images/ingredients/${ingredient}.png`;
        image.onerror = function() {
            this.src = "https://via.placeholder.com/80?text=No+Image";
        };

        let input = document.createElement("input");
        input.type = "text";
        input.value = ingredient;
        input.addEventListener("input", () => updateIngredient(ingredient, input.value));

        let deleteButton = document.createElement("button");
        deleteButton.innerText = "❌";
        deleteButton.onclick = function() {
            deleteIngredient(ingredientCard);
        };

        ingredientCard.appendChild(image);
        ingredientCard.appendChild(input);
        ingredientCard.appendChild(deleteButton);
        grid.appendChild(ingredientCard);
    });
}

function updateIngredient(oldValue, newValue) {
    console.log(`Updated ${oldValue} to ${newValue}`);
}

function deleteIngredient(card) {
    card.remove();
}
