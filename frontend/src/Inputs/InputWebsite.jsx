import { useCallback, useEffect } from 'react';
import { Field, useFormikContext } from 'formik';
import './InputContainer.scss';
import InputContainer from './InputContainer';

export default function InputWebsite() {
  const { values, setFieldValue } = useFormikContext();
  // const { values, setFieldValue, errors } = useFormikContext();

  // не даём пользователю нажать пробел в начале и конце строки
  useEffect(() => {
    setFieldValue('blog_url', values.blog_url.trim());
  }, [values.blog_url, setFieldValue]);

  const validatePosition = useCallback((value) => {
    if (!value) {
      return 'Поле не может быть пустым';
    }
    if (value.length < 1 || value.length > 200) {
      return 'Должно быть не менее 1 и не более 200 символов';
    }
    if (!/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)/.test(value)) {
      return 'Ссылка должна быть в формате https://example.com';
    }
    return null; // Возвращаем null, если ошибок нет
  }, []);

  return (
    <InputContainer labelText="Ссылка на блог или соцсеть" inputId="blog_url">
      <Field
        id="blog_url"
        type="url"
        name="blog_url"
        className="input"
        validate={validatePosition}
        maxLength={200}
        placeholder="Введите ссылку на блог или соцсеть"
      />
    </InputContainer>
  );
}
