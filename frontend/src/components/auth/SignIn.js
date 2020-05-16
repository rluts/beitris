import React, {useState} from 'react';
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import {Link, Redirect} from "react-router-dom";
import {makeStyles} from "@material-ui/core/styles";
import BaseAuth from "./BaseAuth"


const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  error: {
    color: 'red'
  }
}));

export default function SignIn(props) {
  const classes = useStyles()
  const [values, setValues] = useState({email: '', password: '', rememberMe: false})

  const handleInputChange = e => {
    const {name, value} = e.target
    setValues({...values, [name]: value})
  }

  const authenticate = e => {
      e.preventDefault()
      props.authenticate(values.email, values.password, values.rememberMe)
  }

  if (props.authorized) {
      return (
          <Redirect to="/quiz"/>
      )
  }

  return (
    <BaseAuth title="Sign In">
        <form className={classes.form} noValidate onSubmit={authenticate}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              onChange={handleInputChange}
              value={values.email}
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              onChange={handleInputChange}
              value={values.password}
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              onChange={handleInputChange}
              value={values.rememberMe}
              label="Remember me"
            />
            <Button
              fullWidth
              type="submit"
              variant="contained"
              color="primary"
              className={classes.submit}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                <Link to="#" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link to="/register/" variant="body2">
                  {"Does not have account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
        </form>
    </BaseAuth>
  )
}
