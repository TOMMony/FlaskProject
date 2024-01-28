
const button = document.getElementById('level-up');
const display = document.getElementById('level'); 

button.addEventListener('click', levelUp);

function levelUp() {
level++;
display.innerHTML = level;

if(level >=10){
    image.src = "https://media.tenor.com/2l4-h42qnmcAAAAi/toothless-dancing-toothless.gif"
}
}

