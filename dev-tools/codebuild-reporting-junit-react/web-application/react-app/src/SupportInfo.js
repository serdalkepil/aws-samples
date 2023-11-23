import installInfo from './installInfo'
const stamp = 'Example Corp 2021'

let SupportInfo = () => (
    <footer>
        <div className="container">
            <p><small>{stamp}</small></p>
            <p style={{display:'none'}}><small>
                Instance Type: {installInfo.instanceType} |
                Instance Id: {installInfo.instanceId} |
                Region: {installInfo.region}<br />
                pipelineId: {installInfo.commitId}
            </small></p>   
        </div>
    </footer>
)
export default SupportInfo