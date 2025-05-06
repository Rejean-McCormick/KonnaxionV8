'use client'

/**
 * Description: Primary maker edit page component
 * Author: Hieu Chu
 */

import { useState } from 'react'
import { Input, Form, Button, Modal, message } from 'antd'
import { CustomFormItem } from '../style'
import api from '../../../api'

const MakerEdit = ({
  form: { getFieldDecorator, validateFields, resetFields },
  visible,
  handleCancel,
  getCurrentMaker,
  editMaker
}) => {
  const [submitting, setSubmitting] = useState(false)

  const {
    firstName,
    lastName,
    nationality,
    birthYear,
    deathYear,
    wikiUrl,
    id
  } = getCurrentMaker()

  const handleOk = e => {
    e.preventDefault()
    validateFields(async (err, values) => {
      if (!err) {
        console.log('Received values of maker form: ', values)
        for (let key in values) {
          if (!values[key]) {
            values[key] = null
          }
        }

        if (values.birthYear) {
          values.birthYear = Number(values.birthYear)
        }
        if (values.deathYear) {
          values.deathYear = Number(values.deathYear)
        }

        values.id = id
        console.log('after maker', values)

        setSubmitting(true)
        try {
          const _result = (await api.patch('/maker', values)).data
          setSubmitting(false)
          editMaker(values)
          handleCancel()
          resetFields()
          message.success('Updated maker details successfully!', 2)
        } catch (e) {
          setSubmitting(false)
          message.error(e.response.data.message)
        }
      }
    })
  }

  return (
    <Modal
      visible={visible}
      title="Edit maker details"
      onOk={handleOk}
      onCancel={handleCancel}
      maskClosable={false}
      footer={[
        <Button key="back" onClick={() => resetFields()}>
          Reset
        </Button>,
        <Button
          key="submit"
          type="primary"
          loading={submitting}
          onClick={handleOk}
        >
          Submit
        </Button>
      ]}
    >
      <Form autoComplete="off">
        <CustomFormItem label="First name" hasFeedback>
          {getFieldDecorator('firstName', {
            rules: [
              {
                required: true,
                whitespace: true,
                message: 'Please fill in the first name!'
              }
            ],
            initialValue: firstName
          })(<Input type="text" placeholder="First name" />)}
        </CustomFormItem>

        <CustomFormItem label="Last name" hasFeedback>
          {getFieldDecorator('lastName', {
            rules: [
              {
                required: true,
                whitespace: true,
                message: 'Please fill in the last name!'
              }
            ],
            initialValue: lastName
          })(<Input type="text" placeholder="Last name" />)}
        </CustomFormItem>

        <CustomFormItem label="Nationality" hasFeedback>
          {getFieldDecorator('nationality', {
            initialValue: nationality
          })(<Input type="text" placeholder="Nationality" />)}
        </CustomFormItem>

        <CustomFormItem label="Born" hasFeedback>
          {getFieldDecorator('birthYear', {
            rules: [
              {
                pattern: '^[0-9]{4}$',
                message: 'Please fill in a valid year!'
              }
            ],
            initialValue: birthYear ? String(birthYear) : ''
          })(<Input type="text" placeholder="Born" />)}
        </CustomFormItem>

        <CustomFormItem label="Passed away" hasFeedback>
          {getFieldDecorator('deathYear', {
            rules: [
              {
                pattern: '^[0-9]{4}$',
                message: 'Please fill in a valid year!'
              }
            ],
            initialValue: deathYear ? String(deathYear) : ''
          })(<Input type="text" placeholder="Passed away" />)}
        </CustomFormItem>

        <CustomFormItem label="Website" hasFeedback>
          {getFieldDecorator('wikiUrl', {
            rules: [
              {
                type: 'url',
                message: 'Please fill in a valid URL!'
              }
            ],
            initialValue: wikiUrl
          })(<Input type="text" placeholder="Website" />)}
        </CustomFormItem>
      </Form>
    </Modal>
  )
}

export default Form.create({
  name: 'maker_edit_form'
})(MakerEdit)
