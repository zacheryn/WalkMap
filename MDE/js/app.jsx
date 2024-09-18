import React, { useState, useEffect } from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

export default function App() {
    return (
        <div>
            This is a temp example.
        </div>
    );
}