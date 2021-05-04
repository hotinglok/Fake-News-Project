import React, { useState } from 'react';
import { Box, Button, Checkbox, FormControl, FormControlLabel, InputLabel, makeStyles, OutlinedInput, Paper, Tabs, Tab } from '@material-ui/core';
import { MuiPickersUtilsProvider, KeyboardDatePicker } from '@material-ui/pickers'
import DateFnsUtils from '@date-io/date-fns';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          {children}
        </Box>
      )}
    </div>
  );
}

export const SearchView = ({ searchKeywords, submitLinks }) => {
  const classes = useStyles();
  const [keywords, setKeywords] = useState('');
  const [link1, setLink1] = useState('');
  const [link2, setLink2] = useState('');
  const [extra_days, setExtraDays] = useState(false);

  const handleKeywords = (event) => {
    setKeywords(event.target.value);
  };
  const handleExtraDays = (event) => {
    setExtraDays(event.target.checked);
  };
  const handleLink1 = (event) => {
    setLink1(event.target.value);
  };
  const handleLink2 = (event) => {
    setLink2(event.target.value);
  };

  const today = new Date()
  const currentDate = today.getFullYear() + '-' + (("0" + (today.getMonth() + 1)).slice(-2)) + '-' + ("0" + (today.getDate())).slice(-2);
  const [selectedDate, setSelectedDate] = useState(currentDate);
  const handleDateChange = (date) => {
    const setDate = date.getFullYear() + '-' + (("0" + (date.getMonth() + 1)).slice(-2)) + '-' + ("0" + (date.getDate())).slice(-2)
    console.log(setDate)
    setSelectedDate(setDate);
  };

  const [active_tab, setActiveTab] = useState(0);
  const handleChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <Paper style={{width: "35rem", height: "26rem"}}>
      <Paper>
        <Tabs
          value={active_tab}
          indicatorColor="primary"
          textColor="primary"
          onChange={handleChange}
          centered
        >
          <Tab label="Search" />
          <Tab label="URL Input" />
        </Tabs>
      </Paper>
      <TabPanel value={active_tab} index={0}>
        <form className={classes.root} noValidate autoComplete="off" style={{display: "flex", flexDirection: "column", maxWidth: '70vW'}}>
          <FormControl variant="outlined">
              <InputLabel htmlFor="keyword-search">Keywords</InputLabel>
              <OutlinedInput id="keyword-search" value={keywords} onChange={handleKeywords} label="Keywords"/>
          </FormControl>
          <FormControl variant="outlined">
            <MuiPickersUtilsProvider utils={DateFnsUtils}>
              <KeyboardDatePicker
                disableToolbar
                variant="inline"
                format="MM/dd/yyyy"
                margin="normal"
                id="date-picker-inline"
                label="Date"
                value={selectedDate}
                inputVariant="outlined"
                onChange={handleDateChange}
                KeyboardButtonProps={{
                  'aria-label': 'change date',
                }}
              />
            </MuiPickersUtilsProvider>
          </FormControl>
          <FormControlLabel
            value="extra_days"
            control={<Checkbox color="primary" checked={extra_days} onChange={handleExtraDays} />}
            label="Extra days"
            labelPlacement="end"
          />
          <Button variant="contained" color="primary" onClick={() => searchKeywords(keywords, selectedDate, extra_days)} style={{height: "3rem"}}>
            Search
          </Button>  
      </form>
    </TabPanel>
    <TabPanel value={active_tab} index={1}>
        <form className={classes.root} noValidate autoComplete="off" style={{display: "flex", flexDirection: "column", maxWidth: '70vW'}}>
          <FormControl variant="outlined" style={{paddingBottom: "1rem"}}>
            <InputLabel htmlFor="link1-input">Link 1</InputLabel>
            <OutlinedInput id="link1-input" value={link1} onChange={handleLink1} label="eg. www.bbc.co.uk/news/..."/>
          </FormControl>
          <FormControl variant="outlined">
            <InputLabel htmlFor="link2-input">Link 2</InputLabel>
            <OutlinedInput id="link2-input" value={link2} onChange={handleLink2} label="eg. www.theguardian.com/uk-news..."/>
          </FormControl>
          <Button variant="contained" color="secondary" onClick={() => submitLinks(link1, link2)} style={{height: "3rem", marginTop: "2rem" }}>
            Analyse
          </Button>  
      </form>
    </TabPanel>
  </Paper>
  );
};

export default SearchView