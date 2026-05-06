const button = document.querySelector('button')
const ul = document.querySelector('ul')

button.addEventListener(('click') , () =>{
	// ul.innerHTML += '<li> yangi xator 😉</li>'
	const li = document.createElement('li')
	li.textContent = 'yangi xator 😉'
	ul.appendChild(li)
})