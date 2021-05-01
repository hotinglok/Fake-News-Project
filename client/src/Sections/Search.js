import React, { useState } from 'react';
import { Button, Checkbox, FormControl, FormControlLabel, InputLabel, makeStyles, OutlinedInput } from '@material-ui/core'

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

const Search = ({ searchKeywords }) => {
  const [keywords, setKeywords] = useState('');
  const [date, setDate] = useState('');
  const [extra_days, setExtraDays] = useState(false);
  const classes = useStyles();

  const handleKeywords = (event) => {
    setKeywords(event.target.value);
  };
  const handleDate = (event) => {
    setDate(event.target.value);
  };
  const handleExtraDays = (event) => {
    setExtraDays(event.target.checked)
  }

  return (
    <form className={classes.root} noValidate autoComplete="off" style={{display: "flex", flexDirection: "column", maxWidth: '70vW'}}>
        <FormControl variant="outlined">
            <InputLabel htmlFor="keyword-search">Keywords</InputLabel>
            <OutlinedInput id="keyword-search" value={keywords} onChange={handleKeywords} label="Keywords" />
        </FormControl>
        <FormControl variant="outlined">
            <InputLabel htmlFor="date-search">Date</InputLabel>
            <OutlinedInput id="date-search" value={date} onChange={handleDate} label="Date" />
        </FormControl>
        <FormControlLabel
          value="extra_days"
          control={<Checkbox color="primary" checked={extra_days} onChange={handleExtraDays} />}
          label="Extra days"
          labelPlacement="end"
        />
        <Button variant="outlined" color="primary" onClick={() => searchKeywords(keywords, date, extra_days)}>
            Search
        </Button>  
    </form>
  );
};

export const SearchView = ({ searchKeywords }) => {
    return (
        <Search searchKeywords={searchKeywords} />
    ); 
  };

export default SearchView