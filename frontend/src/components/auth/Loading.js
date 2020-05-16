import React from 'react';
import { Redirect } from 'react-router-dom'

const Loading = (props) => {

    if (props.statusLoaded) {
        if (props.authorized) {
            return (
                <Redirect to="/quiz"/>
            )
        }
        else {
            return (
                <Redirect to="/login" />
            )
        }
    }
    props.loadStatus()
    return (
        <div className="LoadingBlock">
            <h1>Loading...</h1>
        </div>
    );
};

export default Loading;
