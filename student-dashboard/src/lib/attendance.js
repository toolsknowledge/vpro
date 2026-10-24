import { attendanceTotals } from '../data/attendance.js'

export function attendancePercent({ attended, total } = attendanceTotals) {
  return Math.round((attended / total) * 100)
}
