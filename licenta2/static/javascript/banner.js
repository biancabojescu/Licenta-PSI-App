let slideIndex = 0;
showSlides();
function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");

    // Ascunde toate slide-urile
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    // Începe ciclul slide-urilor
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}
    slides[slideIndex-1].style.display = "block";

    // Activează dot-ul corespunzător
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    dots[slideIndex-1].className += " active";

    setTimeout(showSlides, 5000);
}
