// Function to inject the button
function injectButton() {
    // 1. Check if button already exists
    if (document.getElementById("tubecode-btn")) return;

    // 2. Find the "Subscribe" or "Actions" area on YouTube
    // YouTube changes IDs often, but 'actions' or 'owner' usually works
    const actionsRow = document.querySelector('#actions #top-level-buttons-computed') || 
                       document.querySelector('#owner #subscribe-button');

    if (actionsRow) {
        const btn = document.createElement("button");
        btn.id = "tubecode-btn";
        btn.className = "tubecode-btn";
        btn.innerHTML = `
            <div class="tubecode-spinner" id="tubecode-spinner"></div>
            <span>Snatch Code 🐍</span>
        `;
        
        // Add click listener
        btn.addEventListener("click", handleSnatchClick);

        // Insert neatly next to other buttons
        actionsRow.parentNode.insertBefore(btn, actionsRow);
        console.log("✅ Tube-Code button injected!");
    }
}

async function handleSnatchClick() {
    const btnText = document.querySelector("#tubecode-btn span");
    const spinner = document.getElementById("tubecode-spinner");
    
    // UI: Show Loading
    btnText.innerText = "Extracting...";
    spinner.style.display = "block";
    
    const currentUrl = window.location.href;

    try {
        const response = await fetch("https://tube-code-backend.onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: currentUrl })
        });

        const data = await response.json();

        if (data.code) {
            // Copy to Clipboard
            navigator.clipboard.writeText(data.code);
            
            // UI: Success
            btnText.innerText = "Copied! ✅";
            spinner.style.display = "none";
            
            // Reset after 3 seconds
            setTimeout(() => {
                btnText.innerText = "Snatch Code 🐍";
            }, 3000);
        } else {
            alert("No code found or AI error.");
            btnText.innerText = "Error ❌";
        }

    } catch (err) {
        console.error(err);
        btnText.innerText = "Failed ❌";
        alert("Make sure your Python backend is running!");
    }
}

// 3. YouTube Navigation Handling (The "Single Page App" Fix)
const observer = new MutationObserver(() => {
    // Try to inject whenever the DOM changes (lightweight check)
    injectButton();
});

// Start watching the body for changes
observer.observe(document.body, { childList: true, subtree: true });