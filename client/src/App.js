import React, { useState } from "react";
import AnalysisView from "./Sections/Anaysis"
import axios from 'axios'
import CircularProgress from '@material-ui/core/CircularProgress'
import { SearchView }  from "./Sections/Search"
import { ArticlesView } from "./Sections/Articles"
import { TestView } from "./Sections/Test"
import { ArticleSelectView } from "./Sections/ArticleSelect"
import DummySearch from "./Dummy/SearchResults"
import DummyCompare from "./Dummy/CompareResults"
import DummyAnalysis from "./Dummy/AnalysisResults";

export default function App() {
  return (
    <div className="App">
      <State />
    </div>
  );
}

const State = () => {
  const [searchData, updateSearchData] = useState({});
  const [globalData, updateData] = useState({})
  const [section, updateSection] = useState(0);

  const dummySearchKeywords = ( keywords, date, extra_days ) => {
    const searchTerms = {keywords: keywords, date: date, extra_days: extra_days}
    updateSearchData(searchTerms)
    updateData(DummySearch)
    updateSection(1)
  };

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

  const dummySelectArticle = ( source, article, keywords, date, extra_days ) => {
    console.log(`http://localhost:5000/api/v1.0/test?source=${source}&article=${article}&keywords=${keywords}&date=${date}&extra_days${extra_days}`)
    updateData(DummyCompare)
    updateSection(2);
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

  const dummySubmitLinks = ( link1 , link2  ) => {
    console.log(link1, link2)
    console.log(`http://localhost:5000/api/v1.0/results?link1=${link1}&link2=${link2}`)
    updateSection(3);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", minHeight: "100vH"}}>
      {section === 9 && <TestView data={globalData} selectArticle={selectArticle}/>}
      {section === 3 && <SearchView searchKeywords={dummySearchKeywords}/>}
      {section === 1 && <ArticlesView data={globalData} searchData={searchData} selectArticle={dummySelectArticle}/>}
      {section === 2 && <ArticleSelectView data={DummyCompare} searchData={searchData} submitLinks={dummySubmitLinks}/>}
      {section === 0 && <AnalysisView data={DummyAnalysis} />}
      {section === 4 && <Loading />}
    </div>
  );
};

const Loading = () => {
  return(
    <>
      <header style={{marginTop: "-250px", marginBottom: "20px", fontSize: "50px", textAlign: "center"}}> Loading </header>
      <CircularProgress />
    </>
  )
}