import React, { useState } from "react";
import Analysis from "./Sections/Anaysis"
import axios from 'axios'


export default function App() {
  return (
    <div className="App">
      <State />
    </div>
  );
}
const State = () => {
  const [userData, updateUserData] = useState({});
  const [section, updateSection] = useState(0);
  const fetchUserData = () => {
    axios.get('http://localhost:5000/api/v1.0/test').then(resp => {
      console.log(resp.data);
    });
    const data = { name: "Name", email: "name@email.com" };
    updateUserData(data);
    updateSection(1);
  };
  const compareLinks = () => {
    // call an API
    // const data = fetch(.....)
    updateSection(2);
  };
  return (
    <>
      <Header userData={userData} />
      {section === 0 && <InitialView fetchUserData={fetchUserData} />}
      {section === 1 && (
        <UserView compareLinks={compareLinks}/>
      )}
      {section === 2 && (
        <Analysis/>
      )}
    </>
  );
};
const InitialView = ({ fetchUserData }) => {
  return <button onClick={fetchUserData}>Fetch your data!</button>;
};
const UserView = ({ userData, compareLinks }) => {
  return (
    <>
      <div>{JSON.stringify(userData)}</div>
      <button onClick={compareLinks}>Update the data</button>
    </>
  );
};
const Header = ({ userData }) => {
  return <header>Hi, {userData.name}</header>;
};