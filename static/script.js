let ingredientList = [];

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
    
    console.log("Fetching...");
    fetch("/GPT/send-image", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.ingredients) {
            ingredientList = data.ingredients.map(cleanIngredientName);
            displayIngredients();
            document.getElementById("ingredientsDiv").style.display = "block";
            document.getElementById("preferencesDiv").style.display = "block";
        } else {
            alert("No ingredients detected.");
        }
    })
    .catch(error => console.error("Error:", error));
}

// Removes trailing punctuation
function cleanIngredientName(name) {
    return name.replace(/\.$/, "").trim();
}

// Function to update the ingredient grid dynamically
function displayIngredients() {
    let grid = document.getElementById("ingredientsGrid");
    grid.innerHTML = ""; // Clear existing content

    ingredientList.forEach((ingredient, index) => {
        let card = document.createElement("div");
        card.className = "ingredient-card";

        // Image Element
        let img = document.createElement("img");
        img.src = `https://www.themealdb.com/images/ingredients/${ingredient}.png`;

        // Input Field for Editing
        let input = document.createElement("input");
        input.type = "text";
        input.value = ingredient;
        input.onchange = function () {
            updateIngredient(index, this.value);
        };

        // Delete Button
        let deleteBtn = document.createElement("button");
        deleteBtn.innerText = "❌";
        deleteBtn.onclick = function () {
            deleteIngredient(index);
        };

        // Append elements to card
        card.appendChild(img);
        card.appendChild(input);
        card.appendChild(deleteBtn);
        grid.appendChild(card);
    });
}

// Function to update an ingredient
function updateIngredient(index, newValue) {
    let cleanedValue = cleanIngredientName(newValue);
    console.log(`Updated ${ingredientList[index]} to ${cleanedValue}`);
    ingredientList[index] = cleanedValue;
    displayIngredients(); // Refresh UI for changes
}

// Function to delete an ingredient
function deleteIngredient(index) {
    console.log(`Deleted ${ingredientList[index]}`);
    ingredientList.splice(index, 1); // Remove from list
    displayIngredients(); // Refresh UI
}

// Adds a new ingredient
function addIngredient() {
    let newIngredient = document.getElementById("newIngredient").value.trim();
    if (newIngredient && !ingredientList.includes(newIngredient)) {
        ingredientList.push(newIngredient);
        displayIngredients();
    }
}

// Sends ingredients & preferences to API
function generateRecipes() {
    let dietaryPref = document.getElementById("dietaryPref").value;
    let seasoningPref = document.getElementById("seasoningPref").value;
    let cookingTimePref = document.getElementById("cookingTimePref").value;
    let recipeStylePref = document.getElementById("recipeStylePref").value;

    let userPreferences = {
        "Dietary Preference": dietaryPref,
        "Seasoning Preference": seasoningPref,
        "Cooking Time": cookingTimePref,
        "Recipe Style": recipeStylePref
    };

    let requestData = {
        ingredients: ingredientList,
        preferences: userPreferences
    };

    console.log("requestData = ", requestData);

    fetch("/GPT/send-details", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => console.log("Recipes:", data))
    .catch(error => console.error("Error:", error));
}

// Function to preview the image before uploading
function previewImage(event) {
    let reader = new FileReader();
    reader.onload = function() {
        let preview = document.getElementById("preview");
        let identifyBtn = document.getElementById("identifyBtn");

        preview.src = reader.result;
        preview.style.display = "block";  // Show the preview image
        identifyBtn.style.display = "block"; // Show the identify button
    };
    reader.readAsDataURL(event.target.files[0]);
}