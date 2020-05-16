import {Route, Redirect} from "react-router-dom";
import React from "react";

export default function PrivateRoute({ children, authenticated }) {
  return (
    <Route
      render={({ location }) =>
        authenticated ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: "/login",
              state: { from: location }
            }}
          />
        )
      }
    />
  );
}
