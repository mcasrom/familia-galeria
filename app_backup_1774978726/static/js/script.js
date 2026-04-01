function openModal(src){
    document.getElementById("modal").style.display = "flex";
    document.getElementById("modal-img").src = src;
}

function closeModal(){
    document.getElementById("modal").style.display = "none";
}

function updateTag(filename, tag){
    fetch("/update_tag", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `filename=${filename}&tag=${tag}`
    });
}
