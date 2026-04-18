import React from 'react'

function Login({ setUsername, setPassword, Checking }) {
  return (
    <div>
      <form action="">
        <label htmlFor="">Username</label>
        <input type="text" placeholder='Username' required  onChange={(e) => setUsername(e.target.value)}/>

        <label htmlFor="">Password</label>
        <input type="text" placeholder='Password' required  onChange={(e) => setPassword(e.target.value)}/>

        <button type='submit' onClick={Checking}>Login</button>
      </form>
    </div>
  )
}

export default Login
