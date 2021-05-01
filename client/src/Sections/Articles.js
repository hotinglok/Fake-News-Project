import React, { useState } from 'react';
import { Box, Button, makeStyles, } from '@material-ui/core'

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

const Board = () => {
  const [keywords, setKeywords] = useState('');
  const classes = useStyles();

  const handleKeywords = (event) => {
    setKeywords(event.target.value);
  };

  return (
    <div styles={{display:"grid", gridTemplateColumns:"25% 25% 25% 25%"}}>
        <Box bgcolor="red"></Box>
        <Box bgcolor="red"></Box>
        <Box bgcolor="red"></Box>
        <Box bgcolor="red"></Box>
    </div>
  );
};

export const ArticlesView = () => {
    return (
        <Board>
        </Board>
    ); 
  };

export default ArticlesView