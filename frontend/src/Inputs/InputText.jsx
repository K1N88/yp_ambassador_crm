/* eslint-disable react/jsx-props-no-spreading */
import PropTypes from 'prop-types';
import { useField } from 'formik';
import './InputText.scss';

function InputText({
  label, validationSchema, placeholder, ...props
}) {
  const [field, meta] = useField(props);

  return (
    <div className="text-input__container">
      <label
        htmlFor={props.id || props.name}
        className={`text-input__label ${props.name === 'comment' && 'text-input__label_comment'}`}
      >
        {label}
      </label>
      {props.name === 'comment' ? (
        <textarea
          className="text-input text-input_comment"
          {...field}
          {...props}
          placeholder={placeholder}
        />
      ) : (
        <div className="text-input__wrapper">
          <input
            className="text-input"
        //   className={`text-input ${props.name === 'comment' && 'text-input_comment'}`}
            {...field}
            {...props}
            placeholder={placeholder}
          />
          <span className={`input-container__error ${meta.touched && meta.error ? 'input-container__error_active' : ''}`}>{meta.error}</span>
        </div>
      )}
    </div>
  );
}

InputText.defaultProps = {
  name: '',
  id: '',
  validationSchema: null,
  // placeholder: '',
};

InputText.propTypes = {
  name: PropTypes.string,
  id: PropTypes.string,
  label: PropTypes.string.isRequired,
  validationSchema: PropTypes.func,
  placeholder: PropTypes.string.isRequired,
};

export default InputText;
