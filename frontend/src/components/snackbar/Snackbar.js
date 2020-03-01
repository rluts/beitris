import React from 'react';
import {Snackbar} from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";

export default (props) => {
    return (
        <Snackbar open={props.open} autoHideDuration={6000}>
          <Alert severity={props.success ? "success" : "warning"}>
              {props.success ? "You are right!" : "You are wrong. Try again."}
          </Alert>
        </Snackbar>
)};
