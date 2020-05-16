import React from "react";
import { Link } from "react-router-dom";
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
// import IconButton from '@material-ui/core/IconButton';
// import MenuIcon from '@material-ui/icons/Menu';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
  a: {
    color: "white",
    textDecoration: "none"
  },
  welcomeText: {
    fontSize: ".9rem"
  }
}));

export default function BeitrisLayout(props) {
    const classes = useStyles();
    return (
        <div className="BeitrisContainer">
            <AppBar position="static">
              <Toolbar>
                {/*<IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">*/}
                {/*  <MenuIcon />*/}
                {/*</IconButton>*/}
                <Typography variant="h6" className={classes.title}>
                    <Link className={classes.a} to="/">Beitris</Link>
                </Typography>
                  {props.user ? (

                      <>
                        <span className={classes.welcomeText}>
                            Hi, {`${props.user.first_name} ${props.user.last_name}`}
                        </span>
                        <Button color="inherit" onClick={props.logout}> Logout</Button>
                      </>
                  ) : (
                      <Button color="inherit"><Link className={classes.a} to="/login" > Login</Link></Button>
                  )}

              </Toolbar>
            </AppBar>
            <main>
            {props.children}
            </main>
            </div>
    )
}
