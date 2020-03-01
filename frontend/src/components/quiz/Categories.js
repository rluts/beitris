import React from 'react';
import { Select, MenuItem, FormControl } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  }
}));


const Categories = (props) => {
    const classes = useStyles();

    return (
    <FormControl className={classes.formControl}>
      <Select value={props.category} onChange={props.handleChangeCategory}>
          {   props.categories ?
              props.categories.map((category) =>
              <MenuItem style={{padding: 2}} key={category.id} value={category.id}>{category.name}</MenuItem>
          ) : null }

      </Select>
    </FormControl>
)};

export default Categories;