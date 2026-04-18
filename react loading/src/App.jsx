import { useState } from "react"
import Login from "./Components/Login"
import Loading from "./Components/Loading"
function App() {
  const [users, setUsers] = useState([
    {username: "amirxon", password: "amirxon123"},
    {username: "azamat", password: "azamat123"},
  ])
  const [isLogged, setIsLogged] = useState(false)
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [complating, setComplating] = useState(false)
  console.log(username, password);
  
  const Checking = () => {
    if(users.find((user) => user.username === username && user.password === password)){
      setIsLogged(true) 
      setComplating(true)
    }
    else{
      alert("Login yoki parol xato")
    }
  }
  return (
    <div>
      <Loading setComplating={setComplating} complating={complating}/>
      {!isLogged ? <Login setUsername={setUsername} setPassword={setPassword} Checking={Checking}/> : "Siz muvofaqiyatli kirdingiz"}
    </div>
  )
}

export default App
