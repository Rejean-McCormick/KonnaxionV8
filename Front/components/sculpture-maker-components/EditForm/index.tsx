'use client'

/**
 * Description: Sculpture Edit Page component
 * Author: Hieu Chu
 */

import { CardStyled, ColStyled } from '../style'
import { Row, Modal, Button, Icon, message, notification } from 'antd'
import SculptureEdit from './SculptureEdit'
import Router, { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import api from '../../../api'
import Loading from '../../Loading'
import Error from 'next/error'
import EditImage from './EditImage'
import Head from 'next/head'

const defaultPosition = [-34.40581053569814, 150.87842788963476]
const { confirm } = Modal

const tabList = [
  { key: 'tab1', tab: 'Edit text details' },
  { key: 'tab2', tab: 'Edit images' }
]

const SculptureEditForm = () => {
  const router = useRouter()
  const sculptureId = router.query.id

  const [initialData, setInitialData] = useState({})
  const [makerList, setMakerList] = useState([])
  const [tabKey, setTabKey] = useState('tab1')

  const handleTabChange = key => {
    setTabKey(key)
  }

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const handleDelete = () => {
    confirm({
      title: 'Do you want to remove this sculpture?',
      icon: <Icon type="exclamation-circle" style={{ color: '#ff4d4f' }} />,
      style: { top: 110 },
      maskClosable: true,
      okText: 'Confirm',
      okButtonProps: {
        style: {
          background: '#ff4d4f',
          borderColor: '#ff4d4f'
        }
      },
      onOk: async () => {
        try {
          const _result = await api.delete(`/sculpture/${sculptureId}`)
          message.success('Deleted sculpture successfully!', 2)
          Router.push('/sculptures')
        } catch (error) {
          notification.error({
            message: 'Error',
            description: 'Internal server error.'
          })
        }
      }
    })
  }

  useEffect(() => {
    const fetchInitialForm = async () => {
      try {
        const data = (await api.get(`/sculpture/${sculptureId}`)).data
        if (data.latitude) {
          data.latitude = Number(data.latitude)
        }
        if (data.longitude) {
          data.longitude = Number(data.longitude)
        }
        console.log('init', data)
        setInitialData({ ...data })

        const makerData = (await api.get('/maker/')).data
        console.log('makers', makerData)
        setMakerList(makerData)
      } catch (e) {
        const { statusCode, message } = e.response.data
        setError({
          statusCode,
          message
        })
      }
      setLoading(false)
    }
    fetchInitialForm()
  }, [sculptureId])

  if (loading) return <Loading />
  if (error)
    return <Error statusCode={error.statusCode} title={error.message} />

  initialData.images.sort(
    (a, b) => new Date(a.created).getTime() - new Date(b.created).getTime()
  )

  return (
    <>
      <Head>
        <title>Edit {initialData.name}- UOW Sculptures</title>
      </Head>
      <Row gutter={16}>
        <ColStyled xs={24}>
          <CardStyled
            title={`Edit details for ${initialData.name}`}
            tabList={tabList}
            activeTabKey={tabKey}
            onTabChange={handleTabChange}
            extra={
              <Button icon="delete" type="danger" onClick={handleDelete}>
                Delete
              </Button>
            }
          >
            <div style={{ display: tabKey === 'tab1' ? 'block' : 'none' }}>
              <SculptureEdit
                defaultPosition={defaultPosition}
                initialData={initialData}
                makerList={makerList}
                setMakerList={setMakerList}
              />
            </div>

            <div style={{ display: tabKey === 'tab2' ? 'block' : 'none' }}>
              <EditImage
                accessionId={initialData.accessionId}
                name={initialData.name}
                images={initialData.images.map(img => {
                  let formattedImg = { ...img }
                  formattedImg.uid = img.id
                  formattedImg.url = img.url
                  formattedImg.thumbUrl = img.url
                  formattedImg.preview = img.url
                  formattedImg.status = 'done'
                  return formattedImg
                })}
              />
            </div>
          </CardStyled>
        </ColStyled>
      </Row>
    </>
  )
}

export { SculptureEditForm }
