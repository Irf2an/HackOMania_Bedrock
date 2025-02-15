let ingredientList = [];
let missingImages = [];

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
            missingImages = [];
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

function displayIngredients() {
    console.log("🔵 Starting ingredient display...");

    let grid = document.getElementById("ingredientsGrid");
    grid.innerHTML = ""; // Clear existing content
    let missingImagesList = []; // Collect missing ingredient names
    let imageLoadPromises = []; // Array to track image loads

    console.log("🟡 Current ingredient list:", ingredientList);

    ingredientList.forEach((ingredient, index) => {
        let cleanedName = cleanIngredientName(ingredient);
        console.log(`🟢 Processing ingredient: ${cleanedName} (Index: ${index})`);

        let card = document.createElement("div");
        card.className = "ingredient-card";

        // Image Element
        let img = document.createElement("img");
        let imgLoaded = new Promise((resolve) => {
            img.onload = () => {
                console.log(`✅ Image loaded for ${cleanedName}`);
                resolve();
            };

            img.onerror = () => {
                console.warn(`⚠️ Image not found for ${cleanedName}, adding to missingImagesList`);
                missingImagesList.push(cleanedName);
                resolve();
            };
        });

        imageLoadPromises.push(imgLoaded);
        img.src = `https://www.themealdb.com/images/ingredients/${cleanedName}.png`;

        // Input Field for Editing
        let input = document.createElement("input");
        input.type = "text";
        input.value = cleanedName;
        input.onchange = function () {
            console.log(`📝 Ingredient changed: ${cleanedName} → ${this.value}`);
            updateIngredient(index, this.value);
        };

        // Delete Button
        let deleteBtn = document.createElement("button");
        deleteBtn.innerText = "❌";
        deleteBtn.onclick = function () {
            console.log(`❌ Deleting ingredient: ${cleanedName}`);
            deleteIngredient(index);
        };

        // Append elements to card
        card.appendChild(img);
        card.appendChild(input);
        card.appendChild(deleteBtn);
        grid.appendChild(card);
    });

    // **Wait for all images to load or fail before checking missing images**
    Promise.all(imageLoadPromises).then(() => {
        console.log("🟠 Missing images list:", missingImagesList);
        if (missingImagesList.length > 0) {
            console.log("🔴 Fetching missing images from backend...");
            fetchMissingImages(missingImagesList);
        } else {
            console.log("✅ All images loaded successfully, no missing images.");
        }
    });
}

// Function to fetch missing ingredient images from backend
function fetchMissingImages(missingList) {
    console.log("🔵 Sending missing ingredients request:", JSON.stringify({ missing_ingredients: missingList }));

    fetch("/GPT/missing-url", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ ingredients: missingList })
    })
    .then(response => response.json())
    .then(data => {
        console.log("🟢 Received missing image data from backend:", data);

        // Replace missing images with new URLs from backend
        ingredientList.forEach((ingredient, index) => {
            let cleanedName = cleanIngredientName(ingredient);

            if (data[cleanedName]) {
                let imgElements = document.querySelectorAll(".ingredient-card img");
                console.log(`🔄 Updating image for ${cleanedName} → ${data[cleanedName]}`);
                imgElements[index].src = data[cleanedName]; // Replace broken image
                imgElements[index].style.display = "block"; // Show new image
            }
        });

        console.log("✅ All missing images updated successfully.");
    })
    .catch(error => {
        console.error("🔴 Error fetching missing images:", error);
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

// Function to generate recipes
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

    console.log("📡 Sending data to generate recipe:", requestData);

    fetch("/GPT/send-details", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("✅ Recipe Response:", data);
        displayRecipe(data);
    })
    .catch(error => console.error("🔴 Error generating recipe:", error));
}

// Function to display the recipe properly
// Function to display the recipe properly
function displayRecipe(recipeData) {
    let recipeContainer = document.getElementById("recipeResults");

    if (!recipeContainer) {
        console.error("❌ ERROR: recipeResults div not found!");
        return;
    }

    // Show the recipe container when data is available
    recipeContainer.style.display = "block";

    // Clear previous content
    recipeContainer.innerHTML = "";

    // Recipe Title
    let recipeTitle = document.createElement("h2");
    recipeTitle.innerText = "🍽️ Recommended Recipes";
    recipeContainer.appendChild(recipeTitle);

    // Create recipe grid container
    let recipeList = document.createElement("div");
    recipeList.className = "recipe-grid";

    // Create recipe card
    let recipeCard = document.createElement("div");
    recipeCard.className = "recipe-card";

    // Extract Dish Name
    let dishName = document.createElement("h3");
    dishName.innerText = recipeData.recipes.split("\n\n")[0].replace("Dish Name: ", "");
    recipeCard.appendChild(dishName);

    // Format recipe instructions
    let instructions = document.createElement("p");
    instructions.innerHTML = formatRecipeOutput(recipeData.recipes);
    recipeCard.appendChild(instructions);

    // Append to grid and container
    recipeList.appendChild(recipeCard);
    recipeContainer.appendChild(recipeList);
}

// Function to format recipe text properly
function formatRecipeOutput(recipeText) {
    return recipeText
        .replace(/\n\n/g, "<br><br>") // Preserve paragraph spacing
        .replace(/\n- /g, "<br>🔸 ")  // Bullet points for ingredients
        .replace(/\n[0-9]+\./g, match => `<br><strong>${match.trim()}</strong>`); // Bold step numbers
}


// Helper function to format recipe output
function formatRecipeOutput(recipeText) {
    return recipeText
        .replace(/\n\n/g, "<br><br>") // Preserve paragraph spacing
        .replace(/\n- /g, "<br>🔸 ") // Bullet points for ingredients
        .replace(/\n[0-9]+\./g, match => `<br><strong>${match.trim()}</strong>`); // Step numbers bold
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