const showbtn = document.querySelector('#show-btn')
const modal = document.querySelector('#modal')
const overlay = document.querySelector('#overlay')

const addHidden = () =>{
	modal.classList.add('hidden')
	overlay.classList.add('hidden')
}

const removeHidden = () =>{
	modal.classList.remove('hidden')
	overlay.classList.remove('hidden')
}

showbtn.addEventListener(('click') , () => {
	removeHidden()
})

modal.addEventListener(('click'), ()=>{
	addHidden()
})

overlay.addEventListener(('click'), ()=>{
	addHidden()
})

document.addEventListener(('keydown') , (e) => {
	if(e.key == 'Escape'){
		addHidden()
	}
})