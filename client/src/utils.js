import moment from 'moment';

export function calculateGap(array) {
    return array.map((obj, index) => {
      const currentDate = moment(obj.end_time);
      const nextIndex = index + 1;
      const nextObj = nextIndex < array.length ? array[nextIndex] : null;
      if (nextObj) {
        const nextDate = moment(nextObj.start_time);
        const gapInDays = nextDate.diff(currentDate, 'days');
        return { ...obj, gap: gapInDays };
      } else {
        return { ...obj, gap: 0 }; // Set gap as 0 for the last object
      }
    });
  }

export function formatGap(gapInDays) {
    if (gapInDays === 0) {
      return "";
    }
    let msg = '';
    if (gapInDays < 31) {
      msg = `${gapInDays} days`;
    } else if (gapInDays < 365) {
      const gapInMonths = Math.floor(gapInDays / 30);
      msg = `${gapInMonths} months`;
    } else {
      const gapInYears = Math.floor(gapInDays / 365);
      msg = `${gapInYears} years`;
    }

    return `Gap between jobs: ${msg}`
  }