function startFeature() {
    document.getElementById("loader").style.display = "block";

    fetch("/start-feature")
        .then(response => response.json())
        .then(data => {
            document.getElementById("loader").style.display = "none";
            alert(data.message);
        })
        .catch(error => console.error("Error:", error));
}
// Cursor Glow Effect
// Cursor Glow Effect
const cursor = document.createElement("div");
cursor.setAttribute("id", "cursor");
document.body.appendChild(cursor);

document.addEventListener("mousemove", (e) => {
    cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
});

// Particle Trail Effect
document.addEventListener("mousemove", (e) => {
    const particle = document.createElement("div");
    particle.classList.add("particle");
    document.body.appendChild(particle);

    particle.style.left = `${e.clientX}px`;
    particle.style.top = `${e.clientY}px`;

    setTimeout(() => {
        particle.remove();
    }, 500);
});
