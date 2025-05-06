'use client'

/**
 * Description: Sculpture's trends graph component
 * Author: Hieu Chu
 */

import 'ant-design-pro/lib/Charts/style/index.less'
import {
  ColStyled,
  VisitCard,
  LikeCard,
  CommentCard
} from '../../dashboard-components/'
import { Dropdown, Icon, Menu, DatePicker } from 'antd'

const { RangePicker } = DatePicker

import moment from 'moment'
import { useState, useEffect, useRef } from 'react'
import Loading from '../../Loading'
import Error from 'next/error'
import api from '../../../api'
import { CardStyled, ShadowCard } from '../../dashboard-components/style'

const formatDailyData = rawData => {
  const result = []
  for (let date of Object.keys(rawData)) {
    result.push({
      x: moment(date).format('MMM D YYYY'),
      y: rawData[date]
    })
  }
  // sort in correct order
  result.sort((a, b) => moment(a.x).valueOf() - moment(b.x).valueOf)

  return result
}

const SculptureTrend = ({
  totalLikes,
  totalComments,
  totalVisits,
  sculptureId
}) => {
  const [state, setState] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const defaultEndDate = useRef(moment(new Date())).current
  const defaultStartDate = useRef(moment(defaultEndDate).subtract(7, 'days'))
    .current

  const [startDate, setStartDate] = useState(defaultStartDate)
  const [endDate, setEndDate] = useState(defaultEndDate)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const past = startDate.format('YYYY-MM-DD')
        const today = endDate.format('YYYY-MM-DD')
        const defaultToday = defaultEndDate.format('YYYY-MM-DD')

        const likesPromise = api.get(
          `/stats/likes/sculpture-id/${sculptureId}?fromDate=${past}&toDate=${today}`
        )
        const commentsPromise = api.get(
          `/stats/comments/sculpture-id/${sculptureId}?fromDate=${past}&toDate=${today}`
        )
        const visitPromise = api.get(
          `/stats/visits/sculpture-id/${sculptureId}?fromDate=${past}&toDate=${today}`
        )

        const defaultLikesPromise = api.get(
          `/stats/likes/sculpture-id/${sculptureId}?fromDate=${past}&toDate=${defaultToday}`
        )
        const defaultCommentsPromise = api.get(
          `/stats/comments/sculpture-id/${sculptureId}?fromDate=${past}&toDate=${defaultToday}`
        )
        const defaultVisitsPromise = api.get(
          `/stats/visits/sculpture-id/${sculptureId}?fromDate=${past}&toDate=${defaultToday}`
        )

        const [
          { data: rawLikes },
          { data: rawComments },
          { data: rawVisits },
          { data: rawDefaultLikes },
          { data: rawDefaultComments },
          { data: rawDefaultVisits }
        ] = await Promise.all([
          likesPromise,
          commentsPromise,
          visitPromise,
          defaultLikesPromise,
          defaultCommentsPromise,
          defaultVisitsPromise
        ])

        // format daily data statistics
        const LIKE_DATA = formatDailyData(rawLikes)
        const COMMENT_DATA = formatDailyData(rawComments)
        const VISIT_DATA = formatDailyData(rawVisits)

        const DEFAULT_LIKE_DATA = formatDailyData(rawDefaultLikes)
        const DEFAULT_COMMENT_DATA = formatDailyData(rawDefaultComments)
        const DEFAULT_VISIT_DATA = formatDailyData(rawDefaultVisits)

        const DAILY_VISITS = DEFAULT_VISIT_DATA[DEFAULT_VISIT_DATA.length - 1].y
        const DAILY_VISITS_CHANGE =
          DAILY_VISITS - DEFAULT_VISIT_DATA[DEFAULT_VISIT_DATA.length - 2].y

        const DAILY_LIKES = DEFAULT_LIKE_DATA[DEFAULT_LIKE_DATA.length - 1].y
        const DAILY_LIKES_CHANGE =
          DAILY_LIKES - DEFAULT_LIKE_DATA[DEFAULT_LIKE_DATA.length - 2].y

        const DAILY_COMMENTS =
          DEFAULT_COMMENT_DATA[DEFAULT_COMMENT_DATA.length - 1].y
        const DAILY_COMMENTS_CHANGE =
          DAILY_COMMENTS -
          DEFAULT_COMMENT_DATA[DEFAULT_COMMENT_DATA.length - 2].y
        console.log(DEFAULT_COMMENT_DATA)
        console.log('c:', DAILY_COMMENTS)
        console.log('change:', DAILY_COMMENTS_CHANGE)

        setState(state => ({
          ...state,
          TOTAL_VISITS: totalVisits,
          DAILY_VISITS,
          DAILY_VISITS_CHANGE,
          TOTAL_LIKES: totalLikes,
          DAILY_LIKES,
          DAILY_LIKES_CHANGE,
          TOTAL_COMMENTS: totalComments,
          DAILY_COMMENTS,
          DAILY_COMMENTS_CHANGE,
          VISIT_DATA,
          LIKE_DATA,
          COMMENT_DATA
        }))
      } catch (e) {
        const { statusCode, message } = e.response.data
        setError({
          statusCode,
          message
        })
      }
      setLoading(false)
    }
    fetchData()
  }, [
    defaultEndDate,
    endDate,
    sculptureId,
    startDate,
    totalComments,
    totalLikes,
    totalVisits
  ])

  const dateFormat = 'MMM D YYYY'
  const staticToday = moment(new Date())

  const generateMenu = (startDate, endDate) => {
    const disabledDate = current => {
      return current.valueOf() > staticToday.valueOf()
    }

    return (
      <Menu className="date-menu">
        <RangePicker
          defaultValue={[startDate, endDate]}
          value={[startDate, endDate]}
          format={dateFormat}
          size="large"
          allowClear={false}
          separator="-"
          disabledDate={disabledDate}
          ranges={{
            'Past week': [
              moment(staticToday).subtract(7, 'days'),
              moment(staticToday)
            ],
            'Past 2 weeks': [
              moment(staticToday).subtract(14, 'days'),
              moment(staticToday)
            ],
            'Past month': [
              moment(staticToday).subtract(30, 'days'),
              moment(staticToday)
            ]
          }}
          onChange={date => {
            console.log(date)
            if (date[0].valueOf() !== date[1].valueOf()) {
              console.log('not the same')
              setStartDate(date[0])
              setEndDate(date[1])
            } else {
              console.log('the same')
            }
          }}
        />
      </Menu>
    )
  }

  const {
    TOTAL_VISITS,
    DAILY_VISITS,
    DAILY_VISITS_CHANGE,
    TOTAL_LIKES,
    DAILY_LIKES,
    DAILY_LIKES_CHANGE,
    TOTAL_COMMENTS,
    DAILY_COMMENTS,
    DAILY_COMMENTS_CHANGE,
    VISIT_DATA,
    LIKE_DATA,
    COMMENT_DATA
  } = state

  if (loading) return <Loading />
  if (error)
    return <Error statusCode={error.statusCode} title={error.message} />

  return (
    <CardStyled
      title="Trends"
      extra={
        <Dropdown
          overlay={generateMenu(startDate, endDate)}
          trigger={['click']}
          placement="bottomRight"
        >
          <Icon type="more" />
        </Dropdown>
      }
      type="stats"
      style={{ marginTop: 12 }}
    >
      <ColStyled xs={24}>
        <ShadowCard>
          <LikeCard
            TOTAL_LIKES={TOTAL_LIKES}
            DAILY_LIKES={DAILY_LIKES}
            DAILY_LIKES_CHANGE={DAILY_LIKES_CHANGE}
            LIKE_DATA={LIKE_DATA}
            startDate={startDate}
            endDate={endDate}
          />
        </ShadowCard>
      </ColStyled>

      <ColStyled xs={24}>
        <ShadowCard>
          <CommentCard
            TOTAL_COMMENTS={TOTAL_COMMENTS}
            DAILY_COMMENTS={DAILY_COMMENTS}
            DAILY_COMMENTS_CHANGE={DAILY_COMMENTS_CHANGE}
            COMMENT_DATA={COMMENT_DATA}
            startDate={startDate}
            endDate={endDate}
          />
        </ShadowCard>
      </ColStyled>

      <ColStyled xs={24}>
        <ShadowCard>
          <VisitCard
            TOTAL_VISITS={TOTAL_VISITS}
            DAILY_VISITS={DAILY_VISITS}
            DAILY_VISITS_CHANGE={DAILY_VISITS_CHANGE}
            VISIT_DATA={VISIT_DATA}
            startDate={startDate}
            endDate={endDate}
            SINGLE_SCULPTURE
          />
        </ShadowCard>
      </ColStyled>
    </CardStyled>
  )
}

export default SculptureTrend
