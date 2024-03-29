import React, { useState } from "react";
import AnalysisView from "./Sections/Anaysis"
import axios from 'axios'
import CircularProgress from '@material-ui/core/CircularProgress'
import { SearchView }  from "./Sections/Search"
import { ArticlesView } from "./Sections/Articles"
import { ArticleSelectView } from "./Sections/Select"

export default function App() {
  return (
    <div className="App">
      <State />
    </div>
  );
}

const State = () => {
  const [searchData, updateSearchData] = useState({});
  const [globalData, updateData] = useState({});
  const [section, updateSection] = useState(0);

  const searchKeywords = ( keywords, date, extra_days ) => {
    const searchTerms = {keywords: keywords, date: date, extra_days: extra_days}
    updateSearchData(searchTerms)
    axios.get(`http://localhost:5000/api/v1.0/search?keywords=${keywords}&date=${date}&extra_days=${extra_days}`).then(
      resp => {
        updateData(resp.data);
        updateSection(1);
    });
    updateSection(4)
  };

  const selectArticle = ( source, article, keywords, date, extra_days ) => {
    axios.get(`http://localhost:5000/api/v1.0/test?source=${source}&article=${article}&keywords=${keywords}&date=${date}&extra_days${extra_days}`).then(
      resp => {
        console.log(resp.data);
        updateData(resp.data);
        updateSection(2);
    });
    updateSection(4);
  };

  const submitLinks = ( link1 , link2 ) => {
    axios.get(`http://localhost:5000/api/v1.0/results?link1=${link1}&link2=${link2}`).then(
      resp => {
        console.log(resp.data);
        updateData(resp.data);
        updateSection(3);
    });
    updateSection(4);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", minHeight: "100vH", backgroundColor: "#F2FBFF"}}>
      {section === 0 && <SearchView searchKeywords={searchKeywords} submitLinks={submitLinks}/>}
      {section === 1 && <ArticlesView data={globalData} searchData={searchData} selectArticle={selectArticle}/>}
      {section === 2 && <ArticleSelectView data={globalData} searchData={searchData} submitLinks={submitLinks}/>}
      {section === 3 && <AnalysisView data={globalData}/>}
      {section === 4 && <LoadingView/>}
    </div>
  );
};

const LoadingView = () => {
  return(
    <>
      <header style={{marginTop: "-250px", marginBottom: "20px", fontSize: "50px", textAlign: "center"}}> Loading </header>
      <CircularProgress />
    </>
  )
}
