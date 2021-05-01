import React, { useState } from "react";
import "./styles.css";
import { useState } from "react";
export default function App() {
  return (
    <div className="App">
      <State />
    </div>
  );
}
const State = () => {
  const [userData, updateUserData] = useState({});
  const [stage, updateStage] = useState(0);
  const fetchUserData = () => {
    // call an API
    // const data = fetch(.....)
    const data = { name: "Tom", email: "tom@tom.com" };
    updateUserData(data);
    updateStage(1);
  };
  return (
    <>
      <Header userData={userData} />
      {stage === 0 && <InitialView fetchUserData={fetchUserData} />}
      {stage === 1 && (
        <UserView userData={userData} fetchUserData={fetchUserData} />
      )}
    </>
  );
};
const InitialView = ({ fetchUserData }) => {
  return <button onClick={fetchUserData}>Fetch your data!</button>;
};
const UserView = ({ userData, fetchUserData }) => {
  return (
    <>
      <div>{JSON.stringify(userData)}</div>
      <button onClick={fetchUserData}>Update the data</button>
    </>
  );
};
const Header = ({ userData }) => {
  return <header>Hi, {userData.name}</header>;
};