import React from 'react';
import { Button, TextField } from '@material-ui/core';


const Answer = (props) => (
    <form className="AnswerForm" onSubmit={props.checkAnswer}>
        <TextField id="outlined-basic" label="Answer" value={props.answer} onChange={props.handleChangeAnswer} variant="outlined" autoComplete="off"/>
        <Button type="submit" variant="contained" color="primary" disableElevation>
          Check
        </Button>
        <Button onClick={props.handleSkip}>Next >></Button>
    </form>
);

export default Answer;