const countBtn = document.querySelector('.countBtn button');
let countNum = document.querySelector('.countNum h4');

countBtn.addEventListener('click', countUp);

function countUp(){
    countNum.innerHTML++;
}