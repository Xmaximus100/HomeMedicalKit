console.log("Test js")

const cards = [...document.querySelectorAll('[id^="card-"]')]
console.log(cards)

document.addEventListener('DOMContentLoaded', 
gsap.from(cards, {
    opacity: 0,
    x: -100,
    duration: 1,
    stagger: 1,
    ease: 'power3.out',
    delay: 0.3
}))