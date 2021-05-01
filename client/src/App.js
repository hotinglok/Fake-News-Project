import React, { useState } from "react";
import AnalysisView from "./Sections/Anaysis"
import axios from 'axios'
import { SearchView }  from "./Sections/Search"
import { ArticlesView } from "./Sections/Articles"

export default function App() {
  return (
    <div className="App">
      <State />
    </div>
  );
}
const State = () => {
  const [userData, updateUserData] = useState({});
  const [globalData, updateData] = useState({})
  const [section, updateSection] = useState(0);

  const fetchUserData = () => {
    axios.get(`http://localhost:5000/api/v1.0/test`).then(resp => {
      console.log(resp.data);
    });
    const data = { name: "Name", email: "name@email.com" };
    updateUserData(data);
    updateSection(1);
  };

const searchKeywords = ( keywords, date, extra_days ) => {
  const data = axios.get(`http://localhost:5000/api/v1.0/search?keywords=${keywords}&date=${date}&extra_days=${extra_days}`).then(resp => {
    console.log(resp.data);
  });
  console.log(`http://localhost:5000/api/v1.0/search?keywords=${keywords}&date=${date}&extra_days=${extra_days}`)
  updateData(data)
  updateSection(1);
};

const compareLinks = () => {
  // call an API
  // const data = fetch(.....)
  updateSection(2);
};

  const compareSearchResults = ({ source, article }) => {
    const res = axios.get(`http://localhost:5000/api/v1.0/compare?source=${source}&article=${article}`).then(
      resp => {
        console.log(resp.data);
    });
    updateSection(3);
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", minHeight: "100vH"}}>
      <Header userData={userData} data={globalData} />
      {section === 0 && <SearchView searchKeywords={searchKeywords}/>}
      {section === 1 && (
        <ArticlesView />
      )}
      {section === 2 && (
        <AnalysisView/>
      )}
    </div>
  );
};

// const ArticlesView = ({ data, compareLinks }) => {
//   return (
//     <>
//       <div>{JSON.stringify(data)}</div>
//       <button onClick={compareLinks}>Update the data</button>
//     </>
//   );
// };
const Header = ({ userData }) => {
  return <header>Hi, {userData.name}</header>;
};