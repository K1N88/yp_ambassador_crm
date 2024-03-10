// import { useEffect } from 'react';
import PropTypes from 'prop-types';
import { Formik, Form, Field } from 'formik';
import { useSelector } from 'react-redux';
import {
  getIsAmbassadorDataEditing,
  getIsNewAmbassadorAdding,
  // getIsLoadingAmbassadorData,
  getAmbassadorData,
} from '../../services/selectors/ambassadorSelector';
import AmbassadorSectionTitle from './AmbassadorSectionTitle';
import InputName from '../../Inputs/InputName';
import DropdownField from '../../Inputs/DropdownField';
import InputEmail from '../../Inputs/InputEmail';
import InputPhoneNumber from '../../Inputs/InputPhoneNumber';
import InputWebsite from '../../Inputs/InputWebsite';
// импорт иконок для кнопок
import emailIcon from '../../assets/AmbassadorsPage/email-icon.svg';
import phoneIcon from '../../assets/AmbassadorsPage/phone-icon.svg';
import tgIcon from '../../assets/AmbassadorsPage/telegram-icon.svg';
import linkIcon from '../../assets/AmbassadorsPage/link-icon.svg';
import messageIcon from '../../assets/AmbassadorsPage/message-button-icon.svg';
import './AmbassadorPage.scss';

export default function AmbassadorPersInfo({ handleSubmit }) {
  const studyProgramms = useSelector((state) => state.dropdown.studyProgramms);
  // console.log('studyProgramms', studyProgramms);

  const ambassadorData = useSelector(getAmbassadorData);
  // console.log('ambassadorData', ambassadorData);
  const ambassadorName = `${ambassadorData.name || 'Василий'} ${ambassadorData.patronymic || 'Васильевич'} ${ambassadorData.surname || 'Пупкин'}`;

  const isAmbassadorDataEditing = useSelector(getIsAmbassadorDataEditing);
  const isNewAmbassadorAdding = useSelector(getIsNewAmbassadorAdding);

  const handleMailTo = () => {
    window.location.href = `mailto:${ambassadorData.email || '@mail.ru'}`;
  };

  return (
    <article className="ambassador-page__data">
      {isAmbassadorDataEditing || isNewAmbassadorAdding ? (
        <>
          <Formik
            initialValues={!isNewAmbassadorAdding ? {
              name: ambassadorName || 'Василий Васильевич Пупкин',
            } : {
              name: '',
            }}
            onSubmit={handleSubmit}
          >
            {() => (
              <Form>
                <InputName name="name" />
                <Field>
                  {({ field }) => (
                    <DropdownField
                      // eslint-disable-next-line react/jsx-props-no-spreading
                      {...field}
                      labelText="Программа обучения"
                      options={studyProgramms}
                      // options={options}
                      htmlFor="studyProgramm"
                    />
                  )}
                </Field>
              </Form>
            )}
          </Formik>
          <AmbassadorSectionTitle title="Контакты" />
          <Formik
            initialValues={!isNewAmbassadorAdding ? {
              email: ambassadorData.email || 'vladimir@gmailcom',
              phone: ambassadorData.phone || '+7 999 211 01 01',
              telegram_handle: ambassadorData.telegram_handle || '@telega',
              blog_url: ambassadorData.blog_url || 'pupkinmadeontilda.com',
            } : {
              email: '',
              phone: '',
              telegram_handle: '',
              blog_url: '',
            }}
            onSubmit={handleSubmit}
          >
            {() => (
              <Form className="ambassador-page__info-form">
                <InputEmail />
                <InputPhoneNumber />
                <InputName name="telegram_handle" />
                <InputWebsite />
              </Form>
            )}
          </Formik>
        </>
      ) : (
        <>
          <div className="ambassador-page__info">
            <h2 className="ambassador-page__name">{ambassadorName || 'Василий Васильевич Пупкин'}</h2>
            <p className="ambassador-page__position">{ambassadorData.study_programm?.title || 'UI/UX дизайнер'}</p>
          </div>
          <div className="ambassador-page__info">
            <AmbassadorSectionTitle title="Контакты" />
            <ul className="ambassador-page__contacts-list">
              <li className="ambassador-page__contacts-item">
                <img className="ambassador-page__icon" alt="Иконка несколько конвертов" src={emailIcon} />
                {ambassadorData.email || 'vladimir@gmailcom'}
              </li>
              <li className="ambassador-page__contacts-item">
                <img className="ambassador-page__icon" alt="Иконка с трубкой телефона" src={phoneIcon} />
                {ambassadorData.phone || '+7 999 211 01 01'}
              </li>
              <li className="ambassador-page__contacts-item">
                <img className="ambassador-page__icon" alt="Иконка с бумажным самолетиком" src={tgIcon} />
                {ambassadorData.telegram_handle || '@telega'}
              </li>
              <li className="ambassador-page__contacts-item website">
                <img className="ambassador-page__icon" alt="Иконка со скрепкой" src={linkIcon} />
                <a
                  className="ambassador-page__contacts-link"
                  href={ambassadorData.blog_url || 'pupkinmadeontilda.com'}
                  target="_blank"
                  rel="noreferrer"
                >
                  {ambassadorData.blog_url || 'pupkinmadeontilda.com'}
                </a>
              </li>
            </ul>
          </div>
          <button
            className="ambassador-page__contact-button"
            type="button"
            onClick={handleMailTo}
          >
            <img className="ambassador-page__icon" alt="Иконка с конвертиком" src={messageIcon} />
            Написать
          </button>
        </>
      )}
    </article>
  );
}

AmbassadorPersInfo.propTypes = {
  handleSubmit: PropTypes.func.isRequired,
};
