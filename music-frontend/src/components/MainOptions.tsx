import React, {FunctionComponent} from 'react'
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

type HorizButtonOptions = {
    name: string,
    id: number,
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
                    <Button variant="contained" color="primary">
                        {option.name}
                    </Button>
                </Grid>
            ))}
          </Grid>
        </Grid>
      </Grid> 
    )
}

export default HorizOptionButton;