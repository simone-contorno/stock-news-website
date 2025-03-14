import React from 'react';
import { TextField, InputAdornment } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const SearchBar = ({ onSearch }) => {
  return (
    <TextField
      fullWidth
      variant="outlined"
      placeholder="Search stocks..."
      onChange={(e) => onSearch(e.target.value)}
      sx={{
        mb: 4,
        '& .MuiOutlinedInput-root': {
          backgroundColor: 'background.paper',
          '&:hover': {
            '& > fieldset': {
              borderColor: 'primary.main',
            }
          }
        }
      }}
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon color="action" />
          </InputAdornment>
        ),
      }}
    />
  );
};

export default SearchBar;
