import React, {FunctionComponent} from 'react'
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import { Link } from 'react-router-dom';

type HorizButtonOptions = {
    name: string,
    id: number,
    route: string,
}

type HorizButtonProps = {
    options: HorizButtonOptions[],
}

export const HorizOptionButton: FunctionComponent<HorizButtonProps> = ({options}) => {
    return (
        <Grid container spacing={2}>
        <Grid item xs={12}>
          <Grid container justify="center" spacing={2}>
            {options.map((option) => (
                <Grid key={option.id} item>
                    <Link to={option.route}>
                        <Button variant="contained" color="primary">
                            {option.name}
                        </Button>
                    </Link>
                </Grid>
            ))}
          </Grid>
        </Grid>
      </Grid> 
    )
}

export default HorizOptionButton;